(function (jQuery) {
    var global = this;

    var ActionPlan = Backbone.Model.extend({
        defaults: {
            barriers: "",
            proposals: "",
            finalPlan: ""
        },
        initialize: function (options) {
            if (options) {
                this.set('barriers', options.barriers);
                this.set('proposals', options.proposals);
                this.set('finalPlan', options.finalPlan);
            }
        },
        isPlanEmpty: function () {
            return this.get("barriers").length === 0 && this.get("proposals").length === 0 && this.get("finalPlan").length === 0;
        },
        isPlanValid: function () {
            return this.get("barriers").length > 0 || this.get("proposals").length > 0 || this.get("finalPlan").length > 0;
        },
        clone: function (ap) {
            this.set('barriers', ap.get('barriers'));
            this.set('proposals', ap.get('proposals'));
            this.set('finalPlan', ap.get('finalPlan'));
        },
        as_dict: function () {
            return {
                'barriers': this.get('barriers'),
                'proposals': this.get('proposals'),
                'finalPlan': this.get('finalPlan')
            };
        }
    });
    
    var ActionPlanList = Backbone.Collection.extend({
        model: ActionPlan,
        initialize: function (options) {
            for (var i = 0; options !== undefined && i < options.length; i++) {
                var plan = new ActionPlan(options[i]);
                this.add(plan);
            }
        },
        as_array: function () {
            var archive = [];
            this.forEach(function (item) {
                archive.push(item.as_dict());
            });
            
            return archive;
        }
    });

    var Issue = Backbone.Model.extend({
        defaults : {
            id: "",
            image: "",
            text: "",
            subtext: "",
            example: "",
            ordinality: 0,
            actionPlan: null,
            archive: new ActionPlanList(),
            focus: false,
            editing: false
        },
        initialize: function (options) {
            if (options.state) {
                if (_.has(options.state, 'archive')) {
                    this.set('archive', new ActionPlanList(options.state.archive));
                }
                
                if (_.keys(options.state).length > 1) {
                    var actionPlan = new ActionPlan(options.state);
                    this.set('actionPlan', actionPlan);
                }
            }
        },
        hasActionPlan: function () {
            return this.get("actionPlan") !== null;
        },
        hasValidActionPlan: function () {
            return this.hasActionPlan() && this.get("actionPlan").isPlanValid();
        },
        addActionPlan: function () {
            var actionPlan = new ActionPlan();
            
            // initialize with the last one in the archive, if it exists
            var archive = this.get('archive');
            if (archive.length > 0) {
                actionPlan.clone(archive.at(archive.length - 1));
            }
            
            this.set('actionPlan', actionPlan);
            this.save();
        },
        removeActionPlan: function () {
            if (this.hasValidActionPlan()) {
                this.get("archive").add(this.get("actionPlan"));
            }
            this.set({'editing': false, 'actionPlan': null});
            this.save();
        },
        as_dict: function () {
            var actionPlan = this.get('actionPlan');
            var archive = this.get('archive');
            var d = {};
            
            if (actionPlan) {
                d = actionPlan.as_dict();
            }
            
            if (archive.length > 0) {
                d.archive = archive.as_array();
            }
            
            return d;
        }
    });

    var IssueList = Backbone.Collection.extend({
        model: Issue,
        issueFocus: null,
        setFocus: function (issueId) {
            if (this.issueFocus) {
                this.issueFocus.set({ "focus": false, "editing": false });
            }
            this.issueFocus = this.get(issueId);
            if (this.issueFocus) {
                this.issueFocus.set("focus", true);
            }
        },
        getFocus: function () {
            return this.issueFocus;
        }
    });
    
    var IssueView = Backbone.View.extend({
        events : {},

        initialize : function (options) {
            _.bindAll(this, "render", "onChangeEditing");
            this.model.bind("change", this.render);
            this.model.bind("change:editing", this.onChangeEditing);
            
            this.render();
            
            this.parent = options.parent;
        },
        
        onChangeEditing: function () {
            var elt;
            if (this.model.get("editing")) {
                jQuery("#actionplan_form").show();
                jQuery("div.issue-selector").hide();
                
                elt = jQuery("#actionplan_form input[type=submit]")[0];
                jQuery('html, body').animate({scrollTop: jQuery(elt).offset().top}, 1000);
            } else {
                jQuery("div.issue-selector").show();
                elt = jQuery("#gamebox");
                jQuery('html, body').animate({scrollTop: 0}, 0, function () {
                    jQuery("#actionplan_form").hide('fast');
                });
            }
        },
                
        render: function () {
            if (this.model.get("focus")) {
                jQuery(".issue-number").removeClass("focus");
                jQuery(this.el).addClass("focus");
                
                jQuery("#issue_details div.issue-number").html(this.model.get("ordinality"));
                jQuery("#issue_details img.issue-image").attr("src", this.model.get("image"));
                jQuery("#issue_details div.issue-text").html(this.model.get("text"));
                jQuery("#issue_details div.issue-subtext").html(this.model.get("subtext"));
                jQuery("div#example").html(this.model.get("example"));
            }
            
            if (this.model.hasActionPlan()) {
                jQuery(this.el).addClass("marked");
                jQuery("#actionplan").show();
                jQuery("#actionplan a").html("Make Plan");
                jQuery("#checkbox-personal-issue").attr('checked', 'checked');
            } else {
                jQuery(this.el).removeClass("marked");
                jQuery("#actionplan").hide();
                jQuery("#checkbox-personal-issue").removeAttr('checked');
            }
                
            if (this.model.hasValidActionPlan()) {
                var actionPlan = this.model.get('actionPlan');
                jQuery(this.el).addClass("complete");
                jQuery("textarea#barriers").val(actionPlan.get("barriers"));
                jQuery("textarea#proposals").val(actionPlan.get("proposals"));
                jQuery("textarea#finalPlan").val(actionPlan.get("finalPlan"));
                jQuery("#actionplan a").html("Edit Plan");
            } else {
                jQuery(this.el).removeClass("complete");
                jQuery("textarea#barriers").val("");
                jQuery("textarea#proposals").val("");
                jQuery("textarea#finalPlan").val("");
            }
            
            if (this.model.get("focus")) {
                this.parent.trigger('issueChanged');
            }
        }
    });

    var IssueListView = Backbone.View.extend({
        events : {
            'click div.issue-selector div.issue-number': 'onIssueNumber',
            'click #previous_issue': 'onPreviousIssue',
            'click #next_issue': 'onNextIssue',
            'click input[type=checkbox]': 'onPersonalIssue',
            'click #actionplan': 'onActionPlan',
            'click #actionplan_form input[type=submit]': 'onCloseActionPlan'
        },

        initialize : function (options) {
            _.bindAll(this, "render", "onAddIssue", "onIssueNumber", "onPreviousIssue", "onNextIssue", "onActionPlan", "onCloseActionPlan");
            _.extend(this, Backbone.Events);
            
            this.issues = options.issues;
            this.issues.parent = this;
            this.issues.bind('add', this.onAddIssue);
            this.bind('issueChanged', this.render); // fired by the issues list when selection changes
        },
        
        onAddIssue: function (issue) {
            var id = issue.get("id");
            var elt = jQuery("#" + id)[0];
            new IssueView({ model: issue, el: elt, parent: this }).render();
        },
        
        onIssueNumber: function (evt) {
            var tgt = evt.target || evt.srcElement;
            this.issues.setFocus(tgt);
        },

        onPreviousIssue: function (evt) {
            var a = jQuery(".issue-number.focus").prev(".issue-number");
            if (a.length > 0) {
                this.issues.setFocus(a[0].id);
            }
        },

        onNextIssue: function (evt) {
            var a = jQuery(".issue-number.focus").next(".issue-number");
            if (a.length > 0) {
                this.issues.setFocus(a[0].id);
            }
        },

        onPersonalIssue: function (evt) {
            var issue = this.issues.getFocus();
            var checked = jQuery("#checkbox-personal-issue").is(':checked');

            if (!checked && issue.hasActionPlan()) {
                issue.removeActionPlan();
            } else if (checked && !issue.hasActionPlan()) {
                issue.addActionPlan();
            }
        },

        onActionPlan: function (evt) {
            var issue = this.issues.getFocus();
            issue.set('editing', true);
        },

        onCloseActionPlan: function (evt) {
            var issue = this.issues.getFocus();
            var actionPlan = issue.get('actionPlan');

            actionPlan.set({ "barriers": jQuery("textarea#barriers").val(),
                             "proposals": jQuery("textarea#proposals").val(),
                             "finalPlan": jQuery("textarea#finalPlan").val()});
            issue.set("editing", false);
            issue.save();
        },

        render: function () {
            var editing = this.issues.getFocus().get('editing');
            
            // enabled/disable next & prev navigation
            var elt = jQuery(".issue-number.focus");
            var a = jQuery(elt).next(".issue-number");
            if (!editing && a.length > 0) {
                jQuery("#next_issue img").show();
            } else {
                jQuery("#next_issue img").hide();
            }

            a = jQuery(elt).prev(".issue-number");
            if (!editing && a.length > 0) {
                jQuery("#previous_issue img").show();
            } else {
                jQuery("#previous_issue img").hide();
            }
        }
    });
    
    var ProblemSolvingGameState = Backbone.View.extend({
        initialize: function (options) {
            var gameState = global.Intervention.getGameVar('problemsolving', {});
            var userState = this.el ? "defaulter" : "regular";
            
            if (!_.has(gameState, userState)) {
                if (!_.has(gameState, userState) && userState === "defaulter" && _.has(gameState, "regular")) {
                    gameState.defaulter = _.clone(gameState.regular);
                } else {
                    gameState[userState] = {};
                }
            }
            
            this.gameState = gameState[userState];
        },
        
        getState: function (id) {
            return _.has(this.gameState, id) ? this.gameState[id] : null;
        },
        
        setState: function (id, obj) {
            this.gameState[id] = obj;
        }
    });
    
    Backbone.sync = function (method, issue, success, error) {
        global.problemSolvingState.setState(issue.get("id"), issue.as_dict());
        
        // Initiate the ajax call to saveState
        global.Intervention.saveState(function (result) {
            if (result.responseText !== "ok") {
                alert("An error occurred while saving your information. Please try again.");
            }
        });
    };

    jQuery(document).ready(function () {
        global.problemSolvingState = new global.GameState({ game: 'problemsolving', el: 'div#defaulter' });
        
        var issues = new IssueList();
        var issueListView = new IssueListView({
            issues: issues,
            el: 'div#gamebox'
        });
        
        jQuery("div.issue").each(function () {
            var options = { 'id': jQuery(this).children("div.name").html() };
            options.state = global.problemSolvingState.getState(options.id);
                
            var issue = new Issue(options);
            issue.set("text", jQuery(this).children("div.text").html());
            issue.set("subtext", jQuery(this).children("div.subtext").html());
            issue.set("example", jQuery(this).children("div.example").html());
            issue.set("image", jQuery(this).children("div.image").html());
            issue.set("ordinality", jQuery(this).children("div.ordinality").html());
            issues.add(issue);
        });
        
        // Select the 1st issue
        issues.setFocus(issues.at(0));
    });
}(jQuery));

(function (jQuery) {
    var global = this;

    var ActionPlan = Backbone.Model.extend({
        defaults: {
            barriers: "",
            proposals: "",
            finalPlan: ""
        },
        isPlanValid: function () {
            return this.get("barriers").length > 0 || this.get("proposals").length > 0 || this.get("finalPlan").length > 0;
        }
    });

    var Issue = Backbone.Model.extend({
        defaults : {
            id: "",
            image: "",
            text: "",
            subtext: "",
            examples: "",
            ordinality: 0,
            actionPlan: null,
            selected: false,
            editing: false
        },
        hasActionPlan: function () {
           return this.get("actionPlan") !== null; 
        },
        hasValidActionPlan: function () {
            return this.hasActionPlan() && this.get("actionPlan").isPlanValid();
        }
    });

    var IssueList = Backbone.Collection.extend({
        model: Issue
    });
    
    var IssueSelectorView = Backbone.View.extend({
        events : {
        },

        initialize : function (options) {
            _.bindAll(this, "render");
            this.model.bind("change", this.render);
            this.render();
        },
                
        render: function () {
            if (this.model.get("selected")) {
                jQuery(".issue-number").removeClass("infocus");
                jQuery(this.el).addClass("infocus");
            }
            
            if (this.model.hasActionPlan()) {
                jQuery(this.el).addClass("marked");
                jQuery("#actionplan a").html("Make Plan");
                jQuery("#checkbox-personal-issue").attr('checked', 'checked');
            } else {
                jQuery(this.el).removeClass("marked");
            }
                
            if (this.model.hasValidActionPlan()) {
                jQuery(this.el).addClass("complete");
                jQuery("textarea#barriers").val(actionPlan.get("barriers"));
                jQuery("textarea#proposals").val(actionPlan.get("proposals"));
                jQuery("textarea#finalPlan").val(actionPlan.get("finalPlan"));
                jQuery("#actionplan a").html("Edit Plan");
             } else {
                jQuery(this.el).removeClass("complete");
            }
            
            jQuery("#issue_details div.issue-number").html(this.model.get("ordinality"));
            jQuery("#issue_details img.issue-image").attr("src", this.model.get("image"));
            jQuery("#issue_details div.issue-text").html(this.model.get("text"));
            jQuery("#issue_details div.issue-subtext").html(this.model.get("subtext"));
            jQuery("div#example").html(this.model.get("example"));
            
            if (this.model.get("editing")) {
                jQuery("#actionplan").show();
            } else {
                jQuery("#actionplan").hide();
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
            'click #actionplan_form input[type=submit]': 'onCloseActionPlan',
            'click div#top-nav-lateral a': 'onNavigate',
            'click div#bottom-nav-lateral a': 'onNavigate'
        },

        initialize : function (options) {
            _.bindAll(this, "render", "onIssueNumber", "onPreviousIssue", "onNextIssue", "onNavigate", "onActionPlan", "onCloseActionPlan", "onAddIssue");

            this.issues = options.issues;
            this.issues.bind('add', this.onAddIssue);
        },
        
        onAddIssue: function (issue) {
            var id = issue.get("id");
            var elt = jQuery("#" + id)[0];
            new IssueSelectorView({ model: issue, el: elt, parent: this });
        },
        
        onIssueNumber: function (evt) {
            // Deselect the old issue number
            var a = jQuery(".issue-number.infocus").prev(".issue-number");
            if (a.length > 0) {
                var issue = this.issues.get(a[0].id);
                issue.set("selected", false);
            }
           
            // Select the new one & init the detail view with same
            var tgt = evt.target || evt.srcElement;
            var selected = this.issues.get(tgt);
            selected.set("selected", true);
        },

        onPreviousIssue: function (evt) {
            var a = jQuery(".issue-number.infocus").prev(".issue-number");
            if (a.length > 0) {
                var issue = this.issues.get(a[0].id);
                issue.set("selected", true);
            }
        },

        onNextIssue: function (evt) {
            var a = jQuery(".issue-number.infocus").next(".issue-number");
            if (a.length > 0) {
                var issue = this.issues.get(a[0].id);
                issue.set("selected", true);
            }
        },

        onPersonalIssue: function (evt) {
            /**
            var issueId = this.model.get("selected");
            var issue = this.issues.get(issueId);

            var checked = jQuery("#checkbox-personal-issue").is(':checked');

            if (!checked) {
                this.model.set("editing_actionplan", false);

                // @todo -- archive out the action plan if a plan is complete
                // don't do this if the plan is empty or partial
                this.actionPlans.archive(issueId);
            } else {
                if (!this.actionPlans.get(issueId)) {
                    var actionPlan = new ActionPlan({id: issueId});
                    actionPlan.save();

                    this.actionPlans.add(actionPlan);
                }
            }
            **/
        },

        onActionPlan: function (evt) {
            //this.model.set("editing_actionplan", true);
        },

        onCloseActionPlan: function (evt) {
            /**
            // transfer information to the action plan & close if valid
            var issueId = this.model.get("selected");
            var actionPlan = this.actionPlans.get(issueId);

            actionPlan.set("barriers", jQuery("textarea#barriers").val());
            actionPlan.set("proposals", jQuery("textarea#proposals").val());
            actionPlan.set("finalPlan", jQuery("textarea#finalPlan").val());

            if (!actionPlan.isPlanValid()) {
                this.model.set("editing_actionplan", false);
            } else {
                actionPlan.save();

                var self = this;

                // Initiate the ajax call to saveState
                global.Intervention.saveState(function (result) {
                    if (result.response !== "ok") {
                        alert("An error occurred while saving your information. Please try again.");
                    } else {
                        self.model.set("editing_actionplan", false);
                    }
                });
            }
            **/
        },

        render: function () {
            // enabled/disable next & prev navigation
            a = jQuery(elt).next(".issue-number");
            if (a.length > 0) {
                jQuery("#next_issue img").show();
            } else {
                jQuery("#next_issue img").hide();
            }

            a = jQuery(elt).prev(".issue-number");
            if (a.length > 0) {
                jQuery("#previous_issue img").show();
            } else {
                jQuery("#previous_issue img").hide();
            }

/**            
            // Represent selected issue if marked as "personal", i.e. has an action plan
            var actionPlan = this.actionPlans.get(issueId);
            if (actionPlan) {
                jQuery("#actionplan").show();
                jQuery("#checkbox-personal-issue").attr('checked', 'checked');
                jQuery(elt).addClass("personal");

                jQuery("textarea#barriers").val(actionPlan.get("barriers"));
                jQuery("textarea#proposals").val(actionPlan.get("proposals"));
                jQuery("textarea#finalPlan").val(actionPlan.get("finalPlan"));
                jQuery("#actionplan a").html("Make Plan");
            } else {
                jQuery("#actionplan").hide();
                jQuery("#checkbox-personal-issue").removeAttr('checked');
                jQuery(elt).removeClass("personal");

                jQuery("textarea#barriers").val("");
                jQuery("textarea#proposals").val("");
                jQuery("textarea#finalPlan").val("");
                jQuery("#actionplan a").html("Make Plan");
            }

            if (this.model.get("editing_actionplan")) {
                jQuery("#actionplan_form").show();
                elt = jQuery("#actionplan_form input[type=submit]")[0];
                jQuery('html, body').animate({scrollTop: jQuery(elt).offset().top}, 1000);
                jQuery("#next_issue img").hide();
                jQuery("#previous_issue img").hide();
                jQuery("div.issue-selector").hide();
                jQuery("div#actionplan").hide();
            } else {
                jQuery("div.issue-selector").show();
                elt = jQuery("#gamebox");
                jQuery('html, body').animate({scrollTop: 0}, 0, function() {
                    jQuery("#actionplan_form").hide('fast');
                });
            }
**/            
        },

        onNavigate: function (evt) {
/**            
            var tgt = evt.target || evt.srcElement;
            if (this.actionPlans.length < 1) {
                evt.preventDefault();
                alert('Please select at least one barrier before continuing.');
            } else {
                // Initiate the ajax call to saveState
                global.Intervention.saveState(function (result) {
                    if (result.responseText !== "ok") {
                        alert("An error occurred while saving your information. Please try again.");
                    } else {
                        // navigate on success
                        window.location = tgt.href;
                        return true;
                    }
                });
            }
            return false;
**/            
        }
    });

    Backbone.sync = function (method, model, success, error) {
        // Sync is called on model.save()
        // Transfer the results back to the game state
        var game_state = global.Intervention.getGameVar('problemsolving', {});

        var id = model.get("id");

        if (!_.has(game_state, id)) {
            game_state[id] = {};
        }

        game_state[id].id = model.get("id");
        game_state[id].barriers = model.get("barriers") || "";
        game_state[id].proposals = model.get("proposals") || "";
        game_state[id].finalPlan = model.get("finalPlan") || "";
    };

    jQuery(document).ready(function () {
        var issues = new IssueList();
        var issueListView = new IssueListView({
            issues: issues,
            el: 'div#contentcontainer'
        });
        
        // pick up the issues from the DOM
        // add on an action plan if it exists
        var gameState = global.Intervention.getGameVar('problemsolving', {});
        jQuery("div.issue").each(function () {
            var issueId = jQuery(this).children("div.name").html();
                
            var issue = new Issue();
            issue.set("id", issueId);
            issue.set("text", jQuery(this).children("div.text").html());
            issue.set("subtext", jQuery(this).children("div.subtext").html());
            issue.set("example", jQuery(this).children("div.example").html());
            issue.set("image", jQuery(this).children("div.image").html());
            issue.set("ordinality", jQuery(this).children("div.ordinality").html());
            
            if (_.has(gameState, issueId)) {
                issue.set("actionPlan", new ActionPlan({
                    "barriers": gameState[issueId].barriers,
                    "proposals": gameState[issueId].proposals,
                    "finalPlan": gameState[issueId].finalPlan
                }));
            }
            issues.add(issue);
        });
        
        var elt = jQuery(".issue-number")[0];
        jQuery(elt).trigger("click");
    });
}(jQuery));

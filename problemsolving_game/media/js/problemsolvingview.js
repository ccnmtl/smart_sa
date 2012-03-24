(function (jQuery) {
    var global = this;
    
    var ActionPlan = Backbone.Model.extend({
        defaults: {
            id: "", // maps to the Issue id
            barriers: "",
            proposals: "",
            finalPlan: ""
        },
        isPlanValid: function () {
            return this.get("barriers").length > 0 || this.get("proposals").length > 0 || this.get("finalPlan").length > 0;
        }

    });
    
    var ActionPlanList = Backbone.Collection.extend({
        model: ActionPlan,
        archive: function (issueId) {
            this.remove(issueId);
        }
    });
    
    var Issue = Backbone.Model.extend({
        defaults : {
            id: "",
            image: "",
            text: "",
            ordinality: 0
        }
    });
    
    var IssueList = Backbone.Collection.extend({
        model: Issue
    });
    
    var BarrierExercise = Backbone.Model.extend({
        defaults : {
            selected: "",
            editing_actionplan: false
        }
    });

    var IssueListView = Backbone.View.extend({
        events : {
            'click a#complete': 'saveState',
            'click div.issue-selector div.issue-number': 'onIssueNumber',
            'click #previous_issue': 'onPreviousIssue',
            'click #next_issue': 'onNextIssue',
            'click input[type=checkbox]': 'onPersonalIssue',
            'click #actionplan': 'onActionPlan',
            'click #actionplan_form input[type=submit]': 'onCloseActionPlan'
        },
        
        initialize : function (options) {
            _.bindAll(this, "render", "onIssueNumber", "onPreviousIssue", "onNextIssue", "saveState", "onActionPlan", "onCloseActionPlan");
            
            this.issues = options.issues;
            
            this.actionPlans = options.actionPlans;
            this.actionPlans.bind('add', this.render);
            this.actionPlans.bind('remove', this.render);
            
            this.model.bind('change', this.render);
        },
        
        onIssueNumber: function (evt) {
            this.model.set("selected", evt.srcElement.id);
        },
        
        onPreviousIssue: function (evt) {
            if (!this.model.get("editing_actionplan")) {
                var a = jQuery(".issue-number.infocus").prev(".issue-number");
                if (a.length > 0) {
                    this.model.set("selected", a[0].id);
                }
            }
        },
        
        onNextIssue: function (evt) {
            if (!this.model.get("editing_actionplan")) {
                var a = jQuery(".issue-number.infocus").next(".issue-number");
                if (a.length > 0) {
                    this.model.set("selected", a[0].id);
                }
            }
        },
        
        onPersonalIssue: function (evt) {
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
                    this.actionPlans.add(new ActionPlan({id: issueId}));
                }
            }
        },
        
        onActionPlan: function (evt) {
            this.model.set("editing_actionplan", true);
        },
        
        onCloseActionPlan: function (evt) {
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
        },
        
        render: function () {
            var a = jQuery(".issue-number.infocus");
            if (a.length > 0) {
                jQuery(a[0]).removeClass("infocus");
            }
            
            // Number selector
            var issueId = this.model.get("selected");
            var elt = jQuery("#" + issueId);
            jQuery(elt).addClass("infocus");
            
            // fill in the appropriate information
            var issue = this.issues.get(issueId);
            jQuery("#issue_details div.issue-number").html(issue.get("ordinality"));
            jQuery("#issue_details img.issue-image").attr("src", issue.get("image"));
            jQuery("#issue_details div.issue-text").html(issue.get("text"));
            
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

            // Represent selected issue if marked as "personal"
            var actionPlan = this.actionPlans.get(issueId);
            if (actionPlan) {
                jQuery("#actionplan").show();
                jQuery("#checkbox-personal-issue").attr('checked', 'checked');
                jQuery(elt).addClass("personal");
                
                jQuery("textarea#barriers").val(actionPlan.get("barriers"));
                jQuery("textarea#proposals").val(actionPlan.get("proposals"));
                jQuery("textarea#finalPlan").val(actionPlan.get("finalPlan"));
                jQuery("#actionplan a").html("Edit Plan");
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
            } else {
                elt = jQuery("#gamebox");
                jQuery('html, body').animate({scrollTop: 0}, 0, function() {
                    jQuery("#actionplan_form").hide('fast');
                });
            }
        },
    
        saveState: function (evt) {
            if (!this.collection.isValid()) {
                evt.preventDefault();
                alert('Please select at least one barrier.');
            } else {
                // Initiate the ajax call to saveState
                global.Intervention.saveState(function (result) {
                    if (result.response !== "ok") {
                        alert("An error occurred while saving your information. Please try again.");
                    } else {
                        // navigate on success
                        window.location = evt.srcElement.href;
                    }
                });
            }
            return false;
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
        // pick up the individual's personal action plans
        var actionPlans = new ActionPlanList();
        var gameState = global.Intervention.getGameVar('problemsolving', {});
        for (var issueId in gameState) {
            actionPlans.add(new ActionPlan({
                                "id": gameState[issueId].id,
                                "barriers": gameState[issueId].barriers,
                                "proposals": gameState[issueId].proposals,
                                "finalPlan": gameState[issueId].finalPlan
            }));
        }
        
        var issues = new IssueList();
        // pick up the issues from the DOM
        jQuery("div.issue").each(function () {
            var issue = new Issue();
            issue.set("id", jQuery(this).children("div.name").html());
            issue.set("text", jQuery(this).children("div.text").html());
            issue.set("image", jQuery(this).children("div.image").html());
            issue.set("ordinality", jQuery(this).children("div.ordinality").html());
            issues.add(issue);
        });
        
        var issueListView = new IssueListView({
            issues: issues,
            actionPlans: actionPlans,
            el: 'div#contentcontainer',
            model: new BarrierExercise({"selected": jQuery(".issue-number")[0].id})
        }).render();
    });
}(jQuery));
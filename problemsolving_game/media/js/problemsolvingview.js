(function (jQuery) {
    var global = this;
    
    var ActionPlan = Backbone.Model.extend({
        defaults: {
            issueId: "",
            personalIssue: "",
            possibleSolutions: "",
            thePlan: ""
        }
    });
    
    var Issue = Backbone.Model.extend({
        defaults : {
            id: "",
            image: "",
            text: "",
            ordinality: 0,
            personal: false
        }
    });
    
    var IssueList = Backbone.Collection.extend({
        model: Issue,
        isValid: function () {
            return this.length < 1;
        }
    });
    
    var BarrierExercise = Backbone.Model.extend({
        defaults : {
            selected: ""
        }
    });
    
    var IssueView = Backbone.View.extend({
        initialize : function (options) {
            _.bindAll(this);
            
            this.parent = options.parent;
            
            this.model.bind('change:personal', this.parent.render);
        },
    });
    
    
    var IssueListView = Backbone.View.extend({
        events : {
            'click a#complete': 'saveState',
            'click div.issue-selector div.issue-number': 'onIssueNumber',
            'click #previous_issue': 'onPreviousIssue',
            'click #next_issue': 'onNextIssue',
            'click input[type=checkbox]': 'onPersonalIssue'
        },
        
        initialize : function (options) {
            _.bindAll(this, "render", "onAddIssue", "onIssueNumber", "onPreviousIssue", "onNextIssue", "saveState");
            
            this.issues = options.issues;
            this.issues.bind('add', this.onAddIssue);
            
            this.model.bind('change:selected', this.render);
        },
        
        onAddIssue: function (issue) {
            new IssueView({ model: issue, parent: this });
        },
        
        onIssueNumber: function (evt) {
            this.model.set("selected", evt.srcElement.id);
        },
        
        onPreviousIssue: function (evt) {
            var a = jQuery(".issue-number.infocus").prev(".issue-number");
            if (a.length > 0) {
                this.model.set("selected", a[0].id);
            }
        },
        
        onNextIssue: function (evt) {
            var a = jQuery(".issue-number.infocus").next(".issue-number");
            if (a.length > 0) {
                this.model.set("selected", a[0].id);
            }
        },
        
        onPersonalIssue: function (evt) {
            var issueId = this.model.get("selected");
            var issue = this.issues.get(issueId);
            issue.set("personal", jQuery("#checkbox-personal-issue").is(':checked'));
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
            if (issue.get("personal")) {
                jQuery("#actionplan").show();
                jQuery("#checkbox-personal-issue").attr('checked', 'checked');
                jQuery(elt).addClass("personal");
            } else {
                jQuery("#actionplan").hide();
                jQuery("#checkbox-personal-issue").removeAttr('checked');
                jQuery(elt).removeClass("personal");
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
        // Don't do a full server-side save on every sync, i.e. global.Intervention.saveState()
        var game_state = global.Intervention.getGameVar('problemsolving', {});
    };

    jQuery(document).ready(function () {
        var barrierExercise = new BarrierExercise();
        
        var issues = new IssueList();
        var issueListView = new IssueListView({
            issues: issues,
            model: barrierExercise,
            el: 'div#contentcontainer'
        });
        
        var gameState = global.Intervention.getGameVar('problemsolving', {});
        
        jQuery("div.issue").each(function () {
            var issue = new Issue();
            issue.set("id", jQuery(this).children("div.name").html());
            issue.set("text", jQuery(this).children("div.text").html());
            issue.set("image", jQuery(this).children("div.image").html());
            issue.set("ordinality", jQuery(this).children("div.ordinality").html());
            issues.add(issue);
        });
        
        barrierExercise.set("selected", jQuery(".issue-number")[0].id);
    });
}(jQuery));
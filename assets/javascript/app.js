(function() {
  var AddProjectForm, AppRouter, Project, ProjectsCollection, ProjectsList, Section;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  this.App = {
    views: {}
  };

  Project = (function() {

    __extends(Project, Backbone.Model);

    function Project() {
      Project.__super__.constructor.apply(this, arguments);
    }

    return Project;

  })();

  ProjectsCollection = (function() {

    __extends(ProjectsCollection, Backbone.Collection);

    function ProjectsCollection() {
      ProjectsCollection.__super__.constructor.apply(this, arguments);
    }

    ProjectsCollection.prototype.model = Project;

    ProjectsCollection.prototype.url = "/api/projects";

    return ProjectsCollection;

  })();

  App.projects = new ProjectsCollection();

  Section = (function() {

    __extends(Section, Backbone.View);

    function Section() {
      Section.__super__.constructor.apply(this, arguments);
    }

    Section.prototype.render = function() {
      $('#content .active').removeClass();
      this.el.addClass('active');
      return this.el;
    };

    return Section;

  })();

  ProjectsList = (function() {

    __extends(ProjectsList, Section);

    function ProjectsList() {
      ProjectsList.__super__.constructor.apply(this, arguments);
    }

    ProjectsList.prototype.template = Handlebars.compile($("#projects_tmpl").html());

    ProjectsList.prototype.el = $('#projects_list');

    ProjectsList.prototype.events = {
      "click .delete": 'deleteProject'
    };

    ProjectsList.prototype.render = function() {
      Section.prototype.render.call(this);
      return this.el.html(this.template({
        'projects': App.projects.toJSON()
      }));
    };

    ProjectsList.prototype.deleteProject = function(evt) {
      var pid, project;
      var _this = this;
      if (confirm('Delete project?')) {
        pid = $.attr(evt.currentTarget, 'data-project');
        project = App.projects.get(pid);
        return project.destroy({
          success: function() {
            return _this.render();
          },
          error: function() {
            return console.error("Can't delete project");
          }
        });
      }
    };

    return ProjectsList;

  })();

  App.views.projects_list = new ProjectsList();

  AddProjectForm = (function() {

    __extends(AddProjectForm, Section);

    function AddProjectForm() {
      AddProjectForm.__super__.constructor.apply(this, arguments);
    }

    AddProjectForm.prototype.el = $('#add_project');

    AddProjectForm.prototype.events = {
      "submit form": 'submit'
    };

    AddProjectForm.prototype.render = function() {
      Section.prototype.render.call(this);
      return this.$('form').trigger('reset');
    };

    AddProjectForm.prototype.submit = function(evt) {
      var field, fields, project, _i, _len;
      fields = this.$('form').serializeArray();
      project = {};
      for (_i = 0, _len = fields.length; _i < _len; _i++) {
        field = fields[_i];
        project[field.name] = field.value;
      }
      return App.projects.create(project, {
        success: function() {
          return App.router.navigate('', true);
        },
        error: function() {
          return console.error(':(');
        }
      });
    };

    return AddProjectForm;

  })();

  App.views.add_project_form = new AddProjectForm();

  AppRouter = (function() {

    __extends(AppRouter, Backbone.Router);

    function AppRouter() {
      AppRouter.__super__.constructor.apply(this, arguments);
    }

    AppRouter.prototype.routes = {
      ".*": "home",
      "add": "addProject"
    };

    AppRouter.prototype.home = function() {
      console.warn('home');
      return App.views.projects_list.render();
    };

    AppRouter.prototype.addProject = function() {
      console.warn('asasd');
      return App.views.add_project_form.render();
    };

    return AppRouter;

  })();

  App.router = new AppRouter();

  $('a').live('click', function(evt) {
    var href;
    href = $.attr(evt.currentTarget, "href");
    if ((href != null ? href.charAt(0) : void 0) === '/') {
      href = href.substr(1);
      App.router.navigate(href, true);
      return false;
    }
  });

  $(function() {
    return Backbone.history.start({
      pushState: true
    });
  });

}).call(this);

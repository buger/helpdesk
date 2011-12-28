(function() {
  var AddProjectForm, AppRouter, Interaction, InteractionsCollection, InteractionsList, Project, ProjectsCollection, ProjectsList, Section, Sidebar;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  this.App = {
    views: {}
  };

  Interaction = (function() {

    __extends(Interaction, Backbone.Model);

    function Interaction() {
      Interaction.__super__.constructor.apply(this, arguments);
    }

    return Interaction;

  })();

  InteractionsCollection = (function() {

    __extends(InteractionsCollection, Backbone.Collection);

    function InteractionsCollection() {
      InteractionsCollection.__super__.constructor.apply(this, arguments);
    }

    InteractionsCollection.prototype.model = Interaction;

    return InteractionsCollection;

  })();

  Project = (function() {

    __extends(Project, Backbone.Model);

    function Project() {
      Project.__super__.constructor.apply(this, arguments);
    }

    Project.prototype.initialize = function() {
      this.interactions = new InteractionsCollection();
      return this.interactions.url = "/api/projects/" + this.id;
    };

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

  App.projects.reset(projects);

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

  InteractionsList = (function() {

    __extends(InteractionsList, Section);

    function InteractionsList() {
      InteractionsList.__super__.constructor.apply(this, arguments);
    }

    InteractionsList.prototype.template = Handlebars.compile($("#interactions_tmpl").html());

    InteractionsList.prototype.el = $('#interactions');

    InteractionsList.prototype.render = function(project_id) {
      var project;
      var _this = this;
      Section.prototype.render.call(this);
      project = App.projects.get(project_id);
      this.el.html(this.template({
        'interactions': project.interactions.toJSON(),
        'project': project.toJSON()
      }));
      return project.interactions.fetch({
        success: function() {
          return _this.el.html(_this.template({
            'interactions': project.interactions.toJSON(),
            'project': project.toJSON()
          }));
        }
      });
    };

    return InteractionsList;

  })();

  App.views.interactions_list = new InteractionsList();

  Sidebar = (function() {

    __extends(Sidebar, Backbone.View);

    function Sidebar() {
      Sidebar.__super__.constructor.apply(this, arguments);
    }

    Sidebar.prototype.template = Handlebars.compile($("#sidebar_tmpl").html());

    Sidebar.prototype.el = $('#sidebar');

    Sidebar.prototype.initialize = function() {
      return this.render();
    };

    Sidebar.prototype.render = function(project_id) {
      var projects;
      projects = App.projects.toJSON();
      projects = _.map(projects, function(p) {
        p.active = project_id === p.id;
        return p;
      });
      return this.el.html(this.template({
        'projects': projects,
        'active_project': project_id
      }));
    };

    return Sidebar;

  })();

  App.views.sidebar = new Sidebar();

  AppRouter = (function() {

    __extends(AppRouter, Backbone.Router);

    function AppRouter() {
      AppRouter.__super__.constructor.apply(this, arguments);
    }

    AppRouter.prototype.routes = {
      ".*": "home",
      "add": "addProject",
      "interactions/:pid": "showInteractions"
    };

    AppRouter.prototype.home = function() {
      App.views.projects_list.render();
      return App.views.sidebar.render();
    };

    AppRouter.prototype.addProject = function() {
      return App.views.add_project_form.render();
    };

    AppRouter.prototype.showInteractions = function(project_id) {
      App.views.interactions_list.render(project_id);
      return App.views.sidebar.render(project_id);
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

  _.defer(function() {
    return Backbone.history.start({
      pushState: true
    });
  });

}).call(this);

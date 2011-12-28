@App = 
	views: {}


class Interaction extends Backbone.Model

class InteractionsCollection extends Backbone.Collection
	model: Interaction


class Project extends Backbone.Model	
	initialize: ->
		@interactions = new InteractionsCollection()
		@interactions.url = "/api/projects/#{@id}"


class ProjectsCollection extends Backbone.Collection

	model: Project

	url: "/api/projects"

App.projects = new ProjectsCollection()
App.projects.reset(projects)


class Section extends Backbone.View

	render: ->
		$('#content .active').removeClass()
		@el.addClass('active')
		@el


class ProjectsList extends Section
	template: Handlebars.compile $("#projects_tmpl").html()

	el: $('#projects_list')	

	events:
		"click .delete": 'deleteProject'


	render: ->
		Section::render.call @

		@el.html @template 'projects': App.projects.toJSON()


	deleteProject: (evt) ->
		if confirm('Delete project?')
			pid = $.attr evt.currentTarget, 'data-project'

			project = App.projects.get(pid)

			project.destroy
				success: => @render()
				error: -> console.error("Can't delete project")


App.views.projects_list = new ProjectsList()


class AddProjectForm extends Section

	el: $('#add_project')	

	events:
		"submit form": 'submit'


	render: ->
		Section::render.call @

		@$('form').trigger('reset')


	submit: (evt) ->
		fields = @$('form').serializeArray()

		project = {}

		for field in fields
			project[field.name] = field.value

		App.projects.create project,
			success: ->
				App.router.navigate('', true)			
			error: ->
				console.error ':('				

App.views.add_project_form = new AddProjectForm()


class InteractionsList extends Section

	template: Handlebars.compile $("#interactions_tmpl").html()

	el: $('#interactions')	


	render: (project_id) ->
		Section::render.call @

		project = App.projects.get(project_id)

		@el.html @template {
			'interactions': project.interactions.toJSON()
			'project': project.toJSON()
		}

		project.interactions.fetch
			success: =>
				@el.html @template {
					'interactions': project.interactions.toJSON()
					'project': project.toJSON()
				}

App.views.interactions_list = new InteractionsList()


class Sidebar extends Backbone.View

	template: Handlebars.compile $("#sidebar_tmpl").html()

	el: $('#sidebar')

	initialize: -> @render()

	render: (project_id) ->
		projects = App.projects.toJSON()
		projects = _.map projects, (p) -> 
			p.active = project_id is p.id
			p

		@el.html @template {
			'projects': projects
			'active_project': project_id
		}		

App.views.sidebar = new Sidebar()



class AppRouter extends Backbone.Router

	routes:
    	".*": "home"
    	"add": "addProject"
    	"interactions/:pid": "showInteractions"

    home: ->     	
    	App.views.projects_list.render()
    	App.views.sidebar.render()

    addProject: ->
    	App.views.add_project_form.render()

    showInteractions: (project_id) ->
    	App.views.interactions_list.render(project_id)
    	App.views.sidebar.render(project_id)
  

App.router = new AppRouter()

$('a').live 'click', (evt) ->
	href = $.attr(evt.currentTarget, "href")

	if href?.charAt(0) is '/'
		href = href.substr(1) 	
		App.router.navigate href, true
		false
	

_.defer -> Backbone.history.start pushState: true
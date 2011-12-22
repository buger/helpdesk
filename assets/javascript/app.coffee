@App = 
	views: {}

class Project extends Backbone.Model	


class ProjectsCollection extends Backbone.Collection

	model: Project

	url: "/api/projects"

App.projects = new ProjectsCollection()


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


class AppRouter extends Backbone.Router

	routes:
    	".*": "home"
    	"add": "addProject"

    home: -> 
    	console.warn 'home' 
    	App.views.projects_list.render()

    addProject: ->
    	console.warn 'asasd'
    	App.views.add_project_form.render()
  

App.router = new AppRouter()

$('a').live 'click', (evt) ->
	href = $.attr(evt.currentTarget, "href")

	if href?.charAt(0) is '/'
		href = href.substr(1) 	
		App.router.navigate href, true
		false
	
$ -> 
	Backbone.history.start pushState: true
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool,ScrapeWebsiteTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class JobListing():
	"""JobListing crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def job_scout(self) -> Agent:
		return Agent(
			config=self.agents_config['job_scout'],
			verbose=True,
			tools=[SerperDevTool()]
		)

	@agent
	def job_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['job_analyzer'],
			verbose=True,
			tools=[ScrapeWebsiteTool()]
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def job_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['job_search_task'],
		)

	@task
	def job_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['job_analysis_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the JobListing crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

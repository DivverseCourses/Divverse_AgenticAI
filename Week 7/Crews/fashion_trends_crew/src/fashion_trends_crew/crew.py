from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class FashionTrendsCrew():
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def retrieve_news(self) -> Agent:
		return Agent(
			config=self.agents_config['retrieve_news'],
			tools=[SerperDevTool(n_results=2)],
			verbose=True
		)

	@agent
	def website_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['website_scraper'],
			tools=[ScrapeWebsiteTool()],
			verbose=True
		)
	
	@agent
	def fashion_news_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['fashion_news_writer'],
			tools=[],
			verbose=True
		)
	
	@agent
	def file_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['file_writer'],
			tools=[FileWriterTool()],
			verbose=True
		)

	@task
	def retrieve_news_task(self) -> Task:
		return Task(
			config=self.tasks_config['retrieve_news_task'],
		)

	@task
	def website_scrape_task(self) -> Task:
		return Task(
			config=self.tasks_config['website_scrape_task'],
		)
	
	@task
	def ai_news_write_task(self) -> Task:
		return Task(
			config=self.tasks_config['fashion_news_write_task'],
		)
	
	@task
	def file_write_task(self) -> Task:
		return Task(
			config=self.tasks_config['file_write_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiNews crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CodeInterpreterTool
from tools.custom_tool import StockRetriever, StringToCode
from dotenv import load_dotenv
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool

load_dotenv()

python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

# Define the manager agent
manager = Agent(
	role="Project Manager",
	goal="Efficiently manage the crew and ensure high-quality task completion from data collection in Yahoo Finance, to model prediction.",
	backstory="You're an experienced project manager, skilled in overseeing complex projects \
			and guiding teams to success. Your role is to coordinate the efforts of the crew members, \
			ensuring that each task is completed on time and to the highest standard.",
	allow_delegation=True,
	)

@CrewBase
class MlCrew():
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def data_retriever(self) -> Agent:
		return Agent(
			config=self.agents_config['data_retriever'],
			verbose=True,
			tools=[StockRetriever()],
		)
	
	@agent
	def data_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['data_analyst'],
			verbose=True,
			tools=[repl_tool]
		)

	@agent
	def ml_engineer(self) -> Agent:
		return Agent(
			config=self.agents_config['ml_engineer'],
			verbose=True,
			tools=[repl_tool]
		)

	@task
	def data_retrieval(self) -> Task:
		return Task(
			config=self.tasks_config['data_retrieval'],
		)

	@task
	def image_plotting_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_plotting_task'],
			output_file='price_plot.png'
		)

	@task
	def trend_communication_task(self) -> Task:
		return Task(
			config=self.tasks_config['trend_communication_task'],
		)

	@task
	def model_training_task(self) -> Task:
		return Task(
			config=self.tasks_config['model_training_task'],
		)

	@crew
	def crew(self) -> Crew:

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.hierarchical,
			verbose=True,
			manager_agent=manager,
		)
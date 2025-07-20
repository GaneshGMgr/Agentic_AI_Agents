from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from software_engineers.llms.ollama_llm import Ollama
import yaml
import os

DEFAULT_TIMEOUT = 600
DEFAULT_RETRIES = 3 

def get_llm(model_name: str):
    model_map = {
        "llama3_2": "llama3.2:latest",
        "llama3": "llama3:latest",
        "deepseek_r1": "deepseek-r1:latest",
        "mistral": "mistral:latest"
    }
    return Ollama(model_name=model_map.get(model_name, "llama3:latest"))

@CrewBase
class EngineeringTeam():
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of crew.py
        config_dir = os.path.join(base_dir, 'config')
        with open(os.path.join(config_dir, 'agents.yaml'), 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open(os.path.join(config_dir, 'tasks.yaml'), 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    @agent
    def engineering_lead(self) -> Agent:
        config = self.agents_config['engineering_lead']
        config["llm"] = get_llm(config["llm"])
        return Agent(config=config, verbose=True)

    @agent
    def backend_engineer(self) -> Agent:
        config = self.agents_config['backend_engineer']
        config["llm"] = get_llm(config["llm"])
        return Agent(
            config=config,
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=DEFAULT_TIMEOUT,
            max_retry_limit=DEFAULT_RETRIES
        )

    @agent
    def frontend_engineer(self) -> Agent:
        config = self.agents_config['frontend_engineer']
        config["llm"] = get_llm(config["llm"])
        return Agent(config=config, verbose=True)

    @agent
    def test_engineer(self) -> Agent:
        config = self.agents_config['test_engineer']
        config["llm"] = get_llm(config["llm"])
        return Agent(
            config=config,
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=DEFAULT_TIMEOUT,
            max_retry_limit=DEFAULT_RETRIES
        )

    @task
    def design_task(self) -> Task:
        return Task(config=self.tasks_config['design_task'])

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config['code_task'])

    @task
    def frontend_task(self) -> Task:
        return Task(config=self.tasks_config['frontend_task'])

    @task
    def test_task(self) -> Task:
        return Task(config=self.tasks_config['test_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

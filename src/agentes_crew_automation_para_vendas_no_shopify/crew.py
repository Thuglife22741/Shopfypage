from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class AgentesCrewAutomationParaVendasNoShopifyCrew():
    """AgentesCrewAutomationParaVendasNoShopify crew"""

    @agent
    def estrutura_organizer(self) -> Agent:
        return Agent(
            config=self.agents_config['estrutura_organizer'],
            tools=[],
        )

    @agent
    def seo_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_copywriter'],
            tools=[],
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            tools=[],
        )


    @task
    def create_structure_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_structure_task'],
            tools=[],
        )

    @task
    def generate_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_content_task'],
            tools=[],
        )

    @task
    def review_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_content_task'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the AgentesCrewAutomationParaVendasNoShopify crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

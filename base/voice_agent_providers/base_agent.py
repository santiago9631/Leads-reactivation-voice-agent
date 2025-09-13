from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract Base Class for voice agent frameworks.
    Defines the common interface for all agents.
    """

    @abstractmethod
    async def make_call(self, recipient: str, message: str):
        """
        Abstract method to make a call.
        Must be implemented by subclasses.
        """
        pass
    
    
    @abstractmethod
    async def handle_webhook_call():
        pass

    @abstractmethod
    def create_agent(self, name: str):
        """
        Abstract method to create an agent.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def update_agent(self, id: str):
        """
        Abstract method to update an agent.
        Must be implemented by subclasses.
        """
        pass

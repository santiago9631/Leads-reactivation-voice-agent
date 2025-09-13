from abc import ABC, abstractmethod


class LeadLoaderBase(ABC):
    available_statuses = ["NEW", "CONTACTED"]

    @abstractmethod
    def fetch_records(self, lead_ids=None, status="NEW"):
        """
        Abstract method to fetch records. Must be implemented by subclasses.
        Should return a list of records matching the status_filter.
        """
        pass

    @abstractmethod
    def update_record(self, lead_id, updates):
        """
        Abstract method to update a record's status. Must be implemented by subclasses.
        """
        pass

from typing import List, Optional

from sqlalchemy.orm import joinedload, selectinload

from app.data.models.association import Association
from app.data.sqla import sqla, try_commit


class AssociationRepository:
    """
    Provides CRUD access to an external data store.
    """

    def get_associations(self) -> List[Association]:
        """
        Gets all the associations in the data store.

        :return: A list of all fetched associations.
        """
        associations = self._get_associations_with_navigation_properties()
        return associations.all()

    def get_association(self, id: int) -> Optional[Association]:
        """
        Gets the association in the data store with the specified id.

        :param id: The id of the association to fetch.

        :return: The fetched association.
        """
        associations = self._get_associations_with_navigation_properties()
        if len(associations.all()) == 0:
            return None
        return associations.get(id)

    def get_association_by_short_name(self, short_name: str) -> Optional[Association]:
        """
        Gets the association in the data store with the specified id.

        :param short_name: The short_name of the association to fetch.

        :return: The fetched association.
        """
        associations = self._get_associations_with_navigation_properties()
        if len(associations.all()) == 0:
            return None
        return associations.filter_by(short_name=short_name).first()

    def add_association(self, association: Association) -> Association:
        """
        Adds a association to the data store.

        :param **kwargs: A keyword args dictionary containing values for the association to add.

        :return: The added association.
        """
        sqla.session.add(association)
        try_commit()
        return association

    def add_associations(self, associations: tuple) -> tuple:
        """
        Adds a collection of association_args dictionaries to the data store.

        :param association_args: The tuple of association keyword args dictionaries to add.

        :return: The added associations.
        """
        for association in associations:
            sqla.session.add(association)
        try_commit()
        return associations

    def update_association(self, association: Association) -> Optional[Association]:
        """
        Updates a association in the data store.

        :param association: The association to update.

        :return: The updated association.
        """
        if not self.association_exists(association.id):
            return association
        association_in_db = self._set_values_of_association_in_db(association)
        sqla.session.add(association_in_db)
        try_commit()
        return association

    def delete_association(self, id: int) -> Optional[Association]:
        """
        Deletes a association from the data store.

        :param id: The id of the association to delete.

        :return: The deleted association.
        """
        if not self.association_exists(id):
            return None
        association = self.get_association(id)
        sqla.session.delete(association)
        try_commit()
        return association

    def association_exists(self, id: int) -> bool:
        """
        Checks to verify whether a specific association exists in the data store.

        :param id: The id of the association to verify.

        :return: True if the association with the specified id exists in the data store; otherwise false.
        """
        return self.get_association(id) is not None

    def _get_associations_with_navigation_properties(self):
        return Association.query.options(
            joinedload(Association.parent),
            selectinload(Association.children),
            joinedload(Association.first_season),
            joinedload(Association.last_season),
        )

    def _set_values_of_association_in_db(self, association: Association) -> Association | None:
        association_in_db = self.get_association(association.id)
        association_in_db.long_name = association.long_name
        association_in_db.short_name = association.short_name
        association_in_db.parent_id = association.parent_id
        association_in_db.first_season_year = association.first_season_year
        association_in_db.last_season_year = association.last_season_year
        return association_in_db

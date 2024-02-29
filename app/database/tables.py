from app.database.metadata.data import metadata
from sqlalchemy import String, Integer, ForeignKey, ARRAY, Column


# Create tables here
class MediaExesizes(metadata):
    __tablename__ = "mediaexesizes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    media = Column(ARRAY(String, as_tuple=True, dimensions=2), nullable=False)
    type = Column(String, ForeignKey("categoryexesizes.type", ondelete="CASCADE"),
                       nullable=False)
    text = Column(String, nullable=True)
    buttons = Column(ARRAY(String, dimensions=3), nullable=True)


class CategoryExesizes(metadata):
    __tablename__ = "categoryexesizes"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)


class RecomendationsType(metadata):
    __tablename__ = "recomendationstype"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

class Recomendations(metadata):
    __tablename__ = "recomendations"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    media = Column(ARRAY(String, as_tuple=True, dimensions=2), nullable=True)
    type = Column(String, ForeignKey("recomendationstype.type", ondelete="CASCADE"),
                       nullable=False)
    text = Column(String, nullable=True)
    buttons = Column(ARRAY(String, dimensions=3), nullable=True)

class TreningTypes(metadata):
    __tablename__ = "treningtypes"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)


class TreningViews(metadata):
    __tablename__ = "treningviews"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    media = Column(ARRAY(String, as_tuple=True, dimensions=2), nullable=True)
    type = Column(String, ForeignKey("treningtypes.type", ondelete="CASCADE"),
                       nullable=False)
    text = Column(String, nullable=True)
    buttons = Column(ARRAY(String, dimensions=3), nullable=True)
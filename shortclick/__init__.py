from .views import app
from .models import graph

try:
	graph.schema.create_uniqueness_constraint("User", "token")
	graph.schema.create_uniqueness_constraint("Tag", "name")
	graph.schema.create_uniqueness_constraint("Website", "uri")
	graph.schema.create_uniqueness_constraint("Webpage", "url")
	graph.schema.create_uniqueness_constraint("Ticket", "token")
	graph.schema.create_uniqueness_constraint("VISITED")
	graph.schema.create_uniqueness_constraint("TRANSIT")
except:
	"Just ignore schema already created."
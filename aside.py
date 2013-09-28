import nodes
from nodes import *

import templated_node
from templated_node import *

import templated
from templated import *

import widgets
import pieces
import element

def set_document(doc):
	element.document = pieces.document = nodes.document = templated_node.document = templated.document = widgets.document = doc
	
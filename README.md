intro
===
requires fresh pyglet from the repo:
hg clone https://code.google.com/p/pyglet/

and a good deal of imagination at the moment

talk to me in #lemonparty on freenode

mockup1: https://github.com/koo5/lemon-operating-language/blob/refugee_branch/mockup1.odt?raw=true

stuff: https://docs.google.com/document/d/1NQCoEghY5rGyEx9tRulQlPz8Do1JPA8O-uoLq3tpTJk/edit




overall
===
using pyglets text features. might outphase it or start hacking on it.
heading are nice, but do we need varying fonts over one line?



templates
===

we can use decode_attributed like decode_attributed('{element xxx}abc'),
instead of the current way of chopping the template into pieces..
closing elements would be nice

output has to be run thru a templating engine that replaces {%element%}
with current element 

get back to the templating branch but use a proper engine

function declarations and calls are missing.   it should allow
parameters inside the function signature like this: To decide what
number is the larger of (N - number) and (M - number):

https://wiki.python.org/moin/Templating






language
===
inspiration:

binops: find the best nodes to ops ratio for our purposes, implement them all

functions: depend on templates?
how many other features can be handled by function calls?

variables : 
theres some figuring out of static vs dynamic scope: http://en.wikipedia.org/wiki/Scope_(computer_science)
nodes that reference variables should probably use both names and object references to the declaring nodes
upon loading or entering, can optionally use reference by name, when refactoring, use object reference....

foreach loop

object types - shrug, just throw them there for now, dont think about a type system, they are crucial for:

boolean adjectives: http://www.ifwiki.org/index.php/Inform_7_for_Programmers/Part_1#Boolean_Adjectives

tables - alternative ast presentation fun starts here!

rules - or here..

or anywhere..


license
===
still dunno how to license this






events
===
document emits post_render
not wise to move the caret in the middle of or before rerendering
document.push_handlers(post_render = self.post_render_move_caret)


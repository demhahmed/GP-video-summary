import inspect
import random
import objgraph
import resource
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


#####################################


class Foo(object):
    def __init__(self):
        self.val = None

    def __str__(self):
        return “foo – val: {0}”.format(self.val)


def f():
    l = []
    for i in range(3):
        foo = Foo()
        # print “id of foo: {0}”.format(id(foo))
        # print “foo is: {0}”.format(foo)
        l.append(foo)
    return l


def main():
    d = {}
    l = f()
    d['k'] = l
    print("list l has {0} objects of type Foo()".format(len(l)))
    objgraph.show_most_common_types()
    objgraph.show_backrefs(random.choice(objgraph.by_type('Foo')),
                           filename="foo_refs.png")

    objgraph.show_refs(d, filename=‘sample-graph.png’)


if __name__ == __main__:
    main()

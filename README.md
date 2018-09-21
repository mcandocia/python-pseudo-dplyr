# pseudo-dplyr-pipes

This is an example of how to implement pipe operator (`%>%` in R) behavior in Python using operator overloading and classes.

To use, simply run

    from pseudo_dplyr import fake
    f = fake()

Then any function defined in the global scope can be made "pipeable" by accessing it as such:

    def myfunc(*args):
        print(args)

    3 >> f.myfunc(4,5,6)
    # should print out 3 4 5 6

You can also access nested attributes with `f`, as well

    class example_class(object):
        @classmethod
        def test_func(cls, *args):
            print(sum(args))
            return(sum(args))

    x = 3 >> f.example_class.test_func(4,5,6) * 4 / 2 + 1 >> f.example_class.test_func(3,4)/9

`f`, or any other initialized `fake` object can use this behavior. Note that an error will be raised if any other operator is used to the left of it.


// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __virtual_inheritance_to_be_exported_hpp__
#define __virtual_inheritance_to_be_exported_hpp__

struct base{
    virtual void do_smth() {}
};

struct derived : virtual public base
{
};    

#endif//__virtual_inheritance_to_be_exported_hpp__

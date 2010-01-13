// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include "global_variables_to_be_exported.hpp"

namespace global_variables{ 

const color const_var = red;
color non_const_var = blue;

data garray[10];
double arr_of_doubles[100];
    
void init_garray(){
    for( int i =0; i < 10; ++i ){
        garray[i].value = -i;
    }
}

}

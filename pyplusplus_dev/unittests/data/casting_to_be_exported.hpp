// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __casting_to_be_exported_hpp__
#define __casting_to_be_exported_hpp__

namespace casting{ 

struct conversion_constructor_t{
   conversion_constructor_t( int a=2, int b=0 )
   : value_a( a* (-1) ), value_b( b * (-1) )
   {}
   int value_a;
   bool value_b;
};

int get_value_a( int a ){
    conversion_constructor_t cc( a );
    return cc.value_a;
}


struct y{};
    
struct x{
    x() 
    : value(0)
    {}
    
    explicit x( int i )
    : value( i )
    {}
    
    x( bool b )
    : value( b )
    {}
    
    operator int() const { return value; }
    
    operator y(){ return y(); }
    
    int value;
};

struct zzzz{
    operator y const() const { return y(); }
};

int identity( int z ){ return z; }

int x_value(const x& d ){ return d.value; }


struct vector{
    vector(){}
    vector( double ){}
    vector( const vector& ){}
};

struct float_vector{
    float_vector(){}
    float_vector( const float_vector& ){}
    float_vector( const vector& ){}
    float_vector( float ){}
};

inline void do_nothing(){
    float_vector( 5.0 );
}
}

#endif//__casting_to_be_exported_hpp__

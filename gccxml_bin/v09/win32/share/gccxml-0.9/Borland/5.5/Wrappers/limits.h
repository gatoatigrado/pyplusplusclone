#if defined(__USING_STD_NAMES__)
# undef __USING_STD_NAMES__
# include_next <limits.h>
# define __USING_STD_NAMES__
#else
# include_next <limits.h>
#endif

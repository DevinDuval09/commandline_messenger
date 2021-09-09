I wanted to figure out how to write an async server
that could handle commands coming from multiple users
simultaneously. The biggest hang up ended up being
coming up with a method to handle input without blocking.
require.config({
    baseUrl: "/static/", // it's needed first slash for this is working
    paths: {
    	'jquery': 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min',
        'd3': 'http://d3js.org/d3.v3.min',
        'd3f': 'javascripts/d3functions',
        'global': 'javascripts/global'
    },
    shim: {
        'jquery': {
            exports: '$'
        },
        'global': {
            deps: ['jquery','d3','d3f'],
        },
    }
});

require(['global']);
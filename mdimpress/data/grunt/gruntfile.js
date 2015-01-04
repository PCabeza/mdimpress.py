module.exports = function(grunt) {
    var MDCALL = "mdimpress {0}";

    /// Utility function to emulate python '{0}'.format(a)
    String.prototype.format=function(){
        var cp = new String(this);
        for(var i=0 ; i<arguments.length ; i++)
            cp=cp.replace('{'+i+'}',arguments[i]);
        return cp;
    }

    grunt.initConfig({
        less: {
            mdimpress: {
                files: [{ expand: true,
			  cwd: "less/",
			  src: ["*.less"],
			  dest: "css/",
			  ext: ".css"}]
            }
        },
        exec: {
            mdimpress: {
                // call mdimpress.py with first .md file found in current folder
                cmd: function() {
                    var f = grunt.file.expand({matchBase:false},"*.md");
                    if(f.length>0) return MDCALL.format(f[0]);
                },
            }
        },
        watch: {
            less: {
                files: "*.less",
                tasks: ["less"]
            },
            exec: {
                files:"*.md",
                tasks: ["exec"]
            },
            livereload: {
                files: ["*.html","*.css"],
                tasks: [],
                options: { livereload: 35729 },
            },
        },
    });

    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);
    grunt.registerTask('default',['exec','less','watch']);
};

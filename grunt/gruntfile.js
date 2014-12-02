module.exports = function(grunt) {
    grunt.initConfig({
        less: {
            mdimpress: {
                files: [{ expand: true, src: ["*.less"], ext: ".css"}]
            }
        },
	exec: {
	    mdimpress: {
		cmd: function() { // call mdimpress.py with first .md file found in current folder
		    var f = grunt.file.expand({matchBase:false},"*.md");
		    if(f.length>0) return "mdimpress.py "+f[0];
		}
	    }
	},
        watch: {
	    less: {
		files: "./*.less",
		tasks: ["less"]
	    },
	    exec: {
		files:"./*.md",
		tasks: ["exec"]
	    }
        }
    });

    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);
    grunt.registerTask('default',['watch']);    
};

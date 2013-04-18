(function() {
  var global = this;
  var util = global.util = {
    applyTmpl : function(tmpl, data) {
      var pattern = /\$\{([a-z,A-Z,_]*)\}/gi;
      var keys = [];
      var rkeys = [];
      while (match = pattern.exec(tmpl)) {
        rkeys.push(match[0]);
        keys.push(match[1]);
      }
      for (var i in keys) {
        if (data.hasOwnProperty(keys[i])) {
          tmpl = tmpl.replace(rkeys[i], data[keys[i]]);
        }
        else {
          console.log('tmplate error:' + keys[i] + 'not found in data');
        }
      }
      return tmpl;
    }
  }
})();  

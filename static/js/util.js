(function() {
  var global = this;
  var util = global.util = {
    applyTmpl : function(tmpl, data) {
      var pattern = /\$\{([a-z,A-Z,_]*)\}/gi;
      var keys = new Array();
      var rkeys = new Array();
      while (match = pattern.exec(tmpl)) {
        rkeys.push(match[0]);
        keys.push(match[1]);
      }
      for (var i in keys) {
        if (data.hasOwnProperty(keys[i])) {
          tmpl = tmpl.replace(rkeys[i], data[keys[i]]);
        }
        else {
          console.log('error:' + keys[i]);
        }
      }
      return $(tmpl);
    }
  }
})();  

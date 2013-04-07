$(function() {
  var global = this;
  var jug = new Juggernaut();
  var model = {
  };
  var util = global.admin = {
    jug: jug,
    clearArticles: function() {
      $('#itemlist').html('');
    },
    itemView: function(item) {
      // TODO: find all in ${}, replace with corresponding field in item
      // create document node
    },
    applyTmpl: function(tmpl, data) {
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
    },
    feedList: $('#feedlist'),
    feedRowHtml: '<tr>' + 
      '<td class=item-check><input type=checkbox name=feed_check value=${feed_id}></td>' +
      '<td>${feed_title}</td>' +
      '<td>${num_stories}</td>' +
      '<td>${num_subscribers}</td>' +
      '<td>${next_scheduled_update}</td>' +
      '<td>${last_update}</td>' +
      '<td>${oldest_story}</td>' +
      '</tr>',
    feedStateColumn:'<td id="state">${state}</td>',
    addToFeedList: function(feed, idx) {
      //feed['row_idx'] = idx;
      css = idx % 2 == 0 ? 'warning': 'info';
      util.applyTmpl(util.feedRowHtml, feed).addClass(css)
        .children('td').eq(1)
        .after(util.applyTmpl(util.feedStateColumn, {'state':'OK'}))
        .end()
        .end()
        .appendTo(util.feedList);
    },
    getStateColumn: function(feed_id) {
    },
    selectFeed: function(feed, obj) {
      util.getArticles(feed);
      if (util.selectedFeed) {
        util.selectedFeed.removeClass('active');
      }
      obj.addClass('active');
      util.selectedFeed = obj;
    },
    getFeedList: function() {
      $.getJSON($SCRIPT_ROOT + '/get_feedlist', {
      }, function(data) {
        $.each(data.feedlist, function(index, feed){
          util.addToFeedList(feed, index);
        });
      });
    },
    keyPressed: function(e) {
      var code = (e.keyCode ? e.keyCode : e.which);
      if (code == 13) {
        util.addFeed();
      }
    },
    fetchHistoryStories: function(feed_ids) {
      $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + '/import/fetch_history_stories',
        data: JSON.stringify({ 'feed_ids': feed_ids }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
          if (data.state == 'ok') {
            $.each(data.feed_states, function(idx, state) {
              if (state) {
                //feed_ids[idx]
              }
            });
          }
        },
        error: function (error) {
          //do something else
        }
      });
    },
    setupActions: function() {
      // detect daemon state
      var daemonRunning = false;
      if (daemonRunning) {
      }
      else {
        $('#feed_update_daemon_action').click(function() {
          alert('start feed update daemon');
        });
      }

      $('#fetch_feed_history_action').click(function() {
        var ids = new Array(); 
        $.each($('[name=feed_check]'), function(idx, cb) {
          if (cb.checked) ids.push(cb.value);
        });
        util.fetchHistoryStories(ids);
      });

      $('#update_feed_action').click(function() {
        alert('update feed');
      });
      $('#all_feeds_check').click(function() {
        var cbs = $('[name=feed_check]');
        for (var i in cbs) {
          cbs[i].checked = $(this)[0].checked;
        }
      });
    },
    subscribeImport: function(src) {
      jug.subscribe('import:' + src, function(data) {
        if (src == 'google-reader') {
        }
        else if (src == 'OPML') {
        }
        else if (src == 'google-reader-history') {
          console.log(data);
        }
        else {
          //error
        }
      });
    },
    init: function() {
      util.setupActions();
      util.getFeedList();
      util.subscribeImport('google-reader-history');
    }
  };
  util.init();
});


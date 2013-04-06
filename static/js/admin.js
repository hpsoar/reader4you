$(function() {
    var util = {
      clearArticles: function() {
        $('#itemlist').html('');
      },
      itemView: function(item) {
        // TODO: find all in ${}, replace with corresponding field in item
        // create document node
      },
      feedRowHtml: '<tr>' + 
        '<td class=item-check><input type=checkbox name=feed_check value=${feed_id}></td>' +
        '<td>${feed_title}</td>' +
        '<td>${num_subscribers}</td>' +
        '<td>${next_scheduled_update}</td>' +
        '<td>${last_update}</td>' +
        '<td>${oldest_story}</td>' +
        '</tr>',
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
        console.log(tmpl);
        return $(tmpl);
      },
      addToFeedList: function(feed, idx) {
        feed['row_idx'] = idx;
        css = idx % 2 == 0 ? 'warning': 'info';
        util.applyTmpl(util.feedRowHtml, feed).addClass(css).appendTo($('#feedlist'));
      },
      selectFeed: function(feed, obj) {
        util.getArticles(feed);
        if (util.selectedFeed) {
          util.selectedFeed.removeClass('active');
        }
        console.log(obj);
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
        console.log($SCRIPT_ROOT + '/import/fetch_history_stories');
        $.ajax({
            type: "POST",
            url: $SCRIPT_ROOT + '/import/fetch_history_stories',
            data: JSON.stringify({ 'feed_ids': feed_ids }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (msg) {
               //do something
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
      init: function() {
        util.setupActions();
        util.getFeedList();
      }
    };
  util.init();
});


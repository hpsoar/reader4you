$(function() {
  var global = this;
  var jug = new Juggernaut();
  var model = global.model = {
    feeds: [],
    reserve: 10,
    waitingRange: [0, 0],
    fetchFeeds: function() {
      // fetch with waitingRange taking into account
      $.getJSON($SCRIPT_ROOT + '/get_feedlist', {
      }, function(data) {
        if (data.state == 'ok') {
          model.feeds = model.feeds.concat(data.feedlist);
        }
        var offset = model.waitingRange[0];
        var end = model.waitingRange[1];

        if (end - offset > 0) {
          var noMore = false;
          if (end > model.feeds.length) {
            end = model.feeds.length;
            noMore = true;
          }
          global.view.displayFeeds(model.feeds.slice(offset, end), offset, noMore);
        }
      });
    },
    getFeeds: function(offset, end) {
      if (end > model.feeds.length) {
        model.waitingRange = [model.feeds.length, end];
      }
      if (end > model.feeds.length + model.reserve) {
        model.fetchFeeds();
      }
      if (end > model.feeds.length) end = model.feeds.length;
      return model.feeds.slice(offset, end);
    },
  };
  var view = global.view = {
    jug: jug,
    clearArticles: function() {
      $('#itemlist').html('');
    },
    itemView: function(item) {
      // TODO: find all in ${}, replace with corresponding field in item
      // create document node
    },
    feedList: $('#feedlist'),
    pageSize: 1000,
    pageIdx: 0,
    feedRowHtml: '<tr id=${feed_id}>' + 
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
      util.applyTmpl(view.feedRowHtml, feed).addClass(css)
        .children('td').eq(1)
        .after(util.applyTmpl(view.feedStateColumn, {'state':'OK'}))
        .end()
        .end()
        .appendTo(view.feedList);
    },
    noMoreFeeds: function() {
    },
    getStateColumn: function(feed_id) {
    },
    displayFeeds: function(feeds, offset, noMore) {
      $.each(feeds, function(idx, feed) {
        view.addToFeedList(feed, offset + idx);
      });
      if (noMore) {
        console.log('no more...');
      }
    },
    loadFeeds: function() {
      var offset = view.pageIdx * view.pageSize;
      var end = offset + view.pageSize;
      var feeds = global.model.getFeeds(offset, end);
      view.displayFeeds(feeds, offset, false);
      if (feeds.length < view.pageSize) {
        // waiting
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
                view.feedList.children('#'+feed_ids[idx]).children('#state').html('Updating...');
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
        view.fetchHistoryStories(ids);
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
          var feedState = view.feedList.children('#'+data.feed_id).children('#state');
          if (data.state == 'ok') {
            // should update the state of feed in model, then the view
            feedState.html('Updated');
          }
          else {
            feedState.html('Error!');
          }
        }
        else {
          //error
        }
      });
    },
    init: function() {
      view.setupActions();
      view.loadFeeds();
      view.subscribeImport('google-reader-history');
    }
  };
  view.init();
});


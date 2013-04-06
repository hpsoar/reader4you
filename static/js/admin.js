$(function() {
    var util = {
      addFeed: function() {
        $.getJSON($SCRIPT_ROOT + '/add_feed', {
          feed_url: $('#feed_url').val()
        }, function(data) {
          if (data.state == 'ok') {
            util.addToFeedList(data.feed);
            util.showArticles(data.feed, data.stories)
          }
          else if (data.state == 'duplication') {
            alert('already added!');
          }
          else {
            alert('error');
          }
          $('#feed_url').val('');
        });
      },
      clearArticles: function() {
        $('#itemlist').html('');
      },
      itemView: function(item) {
        // TODO: find all in ${}, replace with corresponding field in item
        // create document node
      },
      itemHtml: '<div class=article_summary_view>' +
                  '<div class=title>' + 
                      '<a class=link href=${link} >${title}</a>' +
                      '<span class=pubdate>${publish_date}</span>' +
                  '</div>' +
                  '<div class=author>${author}</div>' +
                  '<div>${summary}</div>' + 
                '</div>',
      addArticle: function(item) {
        // TODO: use a template
        $(util.itemHtml.replace('${title}', item.title)
                       .replace('${link}', item.link)
                       .replace('${publish_date}', item.publish_date)
                       .replace('${author}', item.author)
                       .replace('${summary}', item.summary))
        .appendTo($('#itemlist'));
      },
      showArticles: function(feed, items) {
        util.clearArticles();
        $('#feedtitle').attr('href', feed.link);
        $('#feedtitle').html(feed.feed_title);
        $.each(items, function(index, item) {
          util.addArticle(item);
        });
      },
      getArticles: function(feed) {
        $.getJSON($SCRIPT_ROOT + '/get_stories', {
          feed_id: feed.feed_id
        }, function(data) {
          util.showArticles(feed, data.stories);
        });
      },
      feedRowHtml: '<tr>' + 
        '<td>${row_idx}</td>' +
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
          alert('fetch feed history');
        });
        $('#update_feed_action').click(function() {
          alert('update feed');
        });
      },
      init: function() {
        util.setupActions();
        util.getFeedList();
      }
    };
  util.init();
});


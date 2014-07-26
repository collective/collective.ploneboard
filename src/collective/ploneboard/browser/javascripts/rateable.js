if (!log) {
    var log = {
        toggle: function() {},
        move:   function() {},
        resize: function() {},
        clear:  function() {},
        debug:  function() {},
        info:   function() {},
        warn:   function() {},
        error:  function() {},
        profile: function() {}
    };
}
var timeout = 1000;

function prep4JQ(str) {
    /* From JQUERY selector docs: 
     * If you wish to use any of the meta-characters 
     * (#;&,.+*~':"!^$[]()=>|/@ ) as a literal part of a name, 
     * you must escape the character with two backslashes: \\.
     */
    str = str.replace(/\#/g, '\\#');
    str = str.replace(/\;/g, '\\;');
    str = str.replace(/\&/g, '\\&');
    str = str.replace(/\,/g, '\\,');
    str = str.replace(/\./g, '\\.');
    str = str.replace(/\+/g, '\\+');
    str = str.replace(/\*/g, '\\*');
    str = str.replace(/\~/g, '\\~');
    str = str.replace(/\'/g, "\\'");
    str = str.replace(/\:/g, '\\:');
    str = str.replace(/\"/g, '\\"');
    str = str.replace(/\!/g, '\\!');
    str = str.replace(/\^/g, '\\^');
    str = str.replace(/\$/g, '\\$');
    str = str.replace(/\[/g, '\\[');
    str = str.replace(/\]/g, '\\]');
    str = str.replace(/\(/g, '\\(');
    str = str.replace(/\)/g, '\\)');
    str = str.replace(/\=/g, '\\=');
    str = str.replace(/\>/g, '\\>');
    str = str.replace(/\|/g, '\\|');
    str = str.replace(/\//g, '\\/');
    str = str.replace(/\@/g, '\\@');
    return str
}

function upvoteComment(path, tag_id) {
    jQuery.ajax({
        url: '@@rateable_comments_ajax/upvote',
        cache: false,
        timeout: timeout,
        dataType: "json",
        data: {path: path},
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            log.error(textStatus);
            log.error(errorThrown);
        },
        success: function(data) {
            var id = "div#"+prep4JQ(tag_id);
            var rating_element = jQuery(id);
            rating_element.html(data.reply_rating);

            if (data.user_rating == 'up') {
                var id = "#"+prep4JQ(tag_id)+'-uparrow';
                var arrow_element = jQuery(id);
                arrow_element.addClass('comment_arrow_up_clicked');
                arrow_element.removeClass('comment_arrow_up');
                rating_element.addClass('comment_rating_number_clicked')
                rating_element.removeClass('comment_rating_number')
            }
            else {
                var id = "#"+prep4JQ(tag_id)+'-downarrow';
                var arrow_element = jQuery(id);
                arrow_element.addClass('comment_arrow_down');
                arrow_element.removeClass('comment_arrow_down_clicked');
                rating_element.removeClass('comment_rating_number_clicked')
                rating_element.addClass('comment_rating_number')
            }
        }
    });
}

function downvoteComment(path, tag_id) {
    jQuery.ajax({
        url: '@@rateable_comments_ajax/downvote',
        cache: false,
        dataType: "json",
        data: {path: path},
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            log.error(textStatus);
            log.error(errorThrown);
        },
        success: function(data) {
            var id = "div#"+prep4JQ(tag_id);
            var rating_element = jQuery(id);
            rating_element.html(data.reply_rating);

            if (data.user_rating == 'down') {
                var id = "#"+prep4JQ(tag_id)+'-downarrow';
                var arrow_element = jQuery(id);
                arrow_element.removeClass('comment_arrow_down');
                arrow_element.addClass('comment_arrow_down_clicked');
                rating_element.addClass('comment_rating_number_clicked')
                rating_element.removeClass('comment_rating_number')
            }
            else {
                var id = "#"+prep4JQ(tag_id)+'-uparrow';
                var arrow_element = jQuery(id);
                arrow_element.removeClass('comment_arrow_up_clicked');
                arrow_element.addClass('comment_arrow_up');
                rating_element.removeClass('comment_rating_number_clicked')
                rating_element.addClass('comment_rating_number')
            }

        }
    });
}


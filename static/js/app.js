;(function() {

	WebFontConfig = {
		google: {families: ['Open+Sans:400,700:latin']}
	};
	 
	var cb = function() {
		var wf = document.createElement('script');
		wf.src = '//ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
		wf.type = 'text/javascript';
		wf.async = 'true';
		var s = document.getElementsByTagName('script')[0];
		s.parentNode.insertBefore(wf, s);
	};
	 
	var raf = requestAnimationFrame || mozRequestAnimationFrame || webkitRequestAnimationFrame || msRequestAnimationFrame;
	 
	if (raf) {
		raf(cb);
	} else {
		window.addEventListener('load', cb);
	}

	function bind() {
		var destination = $('.content');
		destination.find('a[data-section]').click(function(event) {
				var anchor = $(this);
				event.preventDefault();
				var section = anchor.attr("data-section");
				$("nav a.active").removeClass("active");
				$("nav a[data-section=\"" + section + "\"]").addClass("active")
				var href = anchor.attr("href");
				var title = anchor.attr("title");
				load(href, title);
			});
	}

	function load(content, title) {

		var destination = $('.content');
		var view = destination.attr("data-view");

		var resource = "/fragment" + content;
		var spinner = $(".spinner");

		destination.attr("data-view", content);

		var to = (content != "/work") ? content : "/";

		var started = Date.now();
		var fragment;

		var replacing = true;
		var completed = false;
		var replaced = false;
		var elapsed = 0;

		var latency = 0;
		var stretch = 1;

		var timeout = 315;

		var complete = function() {

			completed = true;
			var elapsed = Date.now() - started;
			if (elapsed > timeout) {
				destination.removeClass("loading");
				spinner.removeClass("active");
			}

			if (to != location.pathname) {
				history.pushState(null, null, to);
			}

		};

		window.setTimeout(function() {
			if (!completed) {
				destination.addClass("loading");
				spinner.addClass("active");
			}
		}, timeout);

		var success = function(data) {
			fragment = $(data);
			replace(fragment);
		};

		var replace = function(fragment) {
			if (!replaced) {
				fragment.find('img').each(function() {
			    	new RetinaImage(this);
			    });
			    fragment.find('a:not(.external)').click(function(event) {
			    	var anchor = $(this);
					event.preventDefault();
					var section = anchor.attr("data-section");
					$("nav a.active").removeClass("active");
					$("nav a[data-section=\"" + section + "\"]").addClass("active")
					var href = anchor.attr("href");
					var title = anchor.attr("title");
					load(href, title);
			    })
				destination.html(fragment);
				bind();
			}
		};

		if (replacing)
			$.ajax({
				url: resource,
				type: "GET",
				dataType: "html",
				success: success,
				complete: complete,
			});
	}

	$('nav a[data-section]').click(function(event) {
		var anchor = $(this);
		event.preventDefault();
		$("a.active").removeClass("active");
		var section = anchor.attr("data-section");
		$("nav a.active").removeClass("active");
		$("nav a[data-section=\"" + section + "\"]").addClass("active")
		var href = anchor.attr("href");
		var title = anchor.attr("title");
		load(href, title);
	});

	window.addEventListener("popstate", function(e) {
		load(location.pathname)
	});

	// todo: use keymaster to make keybindings

	bind();

})();
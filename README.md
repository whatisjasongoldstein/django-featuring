=============================
django-featuring
=============================

For gathering interesting things to feature.

## Setup

Install this, put `django_featuring` in `settings.INSTALLED_APPS`.

If you want to restrict the content types you can feature (and you almost certainly do), add
the allowed ones to your settings file like this:

    FEATURABLE_CONTENT_TYPES = (
        'my_app/my_model',
        'blog/posts',
        'movies/movie',
    )

## Usage

In your template, fetch your dashboard by slug.

    {% get_featured_dashboard 'homepage' as featured %}

Then...

    {% for item featured.things.all %}
        {{ item.render }}
    {% endfor %}

`render` uses the object's app/model name to find a template, so if you're featuring `blog.Post` you'll probably
want to create a template named `featured/blog.post.html` and fill it with something like

    <acticle class="featured-thing">
        <a href="{{ object.get_absolute_url }}"
            <img src="{{ object.image }}">
            <h1>{{ object.title }}</h1>
        </a>
    </article>

or it will fall back to an ugly default.

Of course, you might want to **use one template for everything.** In that case, you can set `DEFAULT_FEATURED_TEMPLATE`
in settings, which will be passed every featured thing as `object`. After that, all you have to do is add some conventional
methods to your models and it will just work.


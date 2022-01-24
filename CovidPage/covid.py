import streamlit as st
import streamlit.components.v1 as components


def make_covid_dashboard():

    dashboard = components.html(
        """
            <div class='tableauPlaceholder' id='viz1642887830638' style='position: relative'><object class='tableauViz'
            style='display:none;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='COVIDDashboard_16406598287530&#47;COVIDDashboard' />
            <param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
            <param name='filter' value='publish=yes' />
        </object></div>
    <script type='text/javascript'>
        var divElement = document.getElementById('viz1642887830638');
        var vizElement = divElement.getElementsByTagName('object')[0];
        vizElement.style.width = '100%';
        vizElement.style.height = '800px';
        var scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """,
        height=800,
    )

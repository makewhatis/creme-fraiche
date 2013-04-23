<%include file="/includes/header.html"/>
<%include file="/includes/nav.html"/>
    <div class="span8">
        <form id="create" action="/admin/teams/create" method="post">
            <fieldset>
                <legend>Create new team</legend>
                
                <label>Teamname</label>
                <input name="teamname" type="text" />

                <button type="submit" class="btn">Submit</button>
            </fieldset>
        </form>
    </div>
<%include file="/includes/footer.html"/>
<%include file="/includes/header.html"/>
<%include file="/includes/nav.html"/>
    <div class="span8">
        <form id="create" action="/admin/users/create" method="post">
            <fieldset>
                <legend>Create new user</legend>
                <label>Username</label>
                <input name="username" type="text">

                <label>Email Address</label>
                <input name="email" type="text">

                <label class="checkbox">
                  <input name="ldap" type="checkbox"> LDAP Auth
                </label>
                <button type="submit" class="btn">Submit</button>
            </fieldset>
        </form>
    </div>
<%include file="/includes/footer.html"/>
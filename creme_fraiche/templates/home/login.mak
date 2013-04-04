<%include file="/includes/header.html"/>
<%include file="/includes/nav.html"/>
    <div class="span8">
        <form id="login" action="/login" method="post">
            <fieldset>
                <legend>Login</legend>
                <label>Username</label>
                <input name="username" type="text">

                <label>Password</label>
                <input name="password" type="password">

                <button type="submit" class="btn">Submit</button>
            </fieldset>
        </form>
    </div>
<%include file="/includes/footer.html"/>
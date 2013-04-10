<%include file="/includes/header.html"/>
<%include file="/includes/nav.html"/>
    <div class="span8">
        <h2>List Users</h2>
        <div class="actions">
            <a href="/admin/users/create">
                <button class="btn btn-info" >Create User</button>
            </a>
        </div>
        <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Userame</th>
                  <th>Full Name</th>
                  <th>Username</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
        % for user in users:
                <tr>
                  <td>${user.id}</td>
                  <td>${user.username}</td>
                  <td>${user.fullname}</td>
                  <td>${user.email}</td>
                  <td><input id="${user.id}" formaction="/admin/user/delete/${user.id}" class="delete" type="button" value="Delete" /></td>
                </tr>
        % endfor               
              </tbody>
            </table>
    </div>
<%include file="/includes/footer.html"/>
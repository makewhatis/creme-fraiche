<%include file="/includes/header.html"/>
    <div class="span8">
        <h2>List Users</h2>

        <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Userame</th>
                  <th>Full Name</th>
                  <th>Username</th>
                </tr>
              </thead>
              <tbody>
        % for user in users:
                <tr>
                  <td>${user.id}</td>
                  <td>${user.username}</td>
                  <td>${user.fullname}</td>
                  <td>${user.email}</td>
                </tr>
        % endfor               
              </tbody>
            </table>
    </div>
<%include file="/includes/footer.html"/>
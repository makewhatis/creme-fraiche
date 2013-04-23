<%include file="/includes/header.html"/>
<%include file="/includes/nav.html"/>
    <div class="span8">
        <h2>List Teams</h2>
        <div class="actions">
            <a href="/admin/teams/create">
                <button class="btn btn-info" >Create Team</button>
            </a>
        </div>
        <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
        % for team in teams:
                <tr>
                  <td>${team.id}</td>
                  <td>${team.name}</td>
                  <td><input id="${team.id}" formaction="/admin/teams/delete/${team.id}" class="delete" type="button" value="Delete" /></td>
                </tr>
        % endfor               
              </tbody>
            </table>
    </div>
<%include file="/includes/footer.html"/>
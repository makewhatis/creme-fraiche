<%include file="/includes/header.html"/>
    <div class="span8">
        <h2>List Teams</h2>

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
                </tr>
        % endfor               
              </tbody>
            </table>
    </div>
<%include file="/includes/footer.html"/>
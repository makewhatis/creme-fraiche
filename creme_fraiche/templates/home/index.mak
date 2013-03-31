<%include file="/includes/header.html"/>
      <h1>${project}</h1>
      <ul>
        %for user in users:
          <li>${user.fullname}</li>
        %endfor
      </ul>
<%include file="/includes/footer.html"/>
<%include file="/includes/header.html"/>
    <div class="span9">
          <h1>${project}</h1>
          <ul>
            %for user in users:
              <li>${user.fullname}</li>
            %endfor
          </ul>
    </div>
<%include file="/includes/footer.html"/>
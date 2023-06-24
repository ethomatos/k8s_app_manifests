docker run -d -e CLIENTID='106028289955-6a7iupv7rbmggop3im2db2o2qit9pleu.apps.googleusercontent.com' \
-e CLIENTSECRET='pGWvkv--9bXCK21m3I4J7LQH' \
-e REFRESHTOKEN='1//0d4wpFIo0A84zCgYIARAAGA0SNwF-L9IrItLAIl1dCclMlT7ekFWelBrJnjcc9qnJdaqscqlII7rTbkZdcDFYNlmb0m7JHSqo-EU' \
-e PROJECTID='17f0511f-e6bb-44e2-a53b-dacb340da87f' \
-e API_KEY='' \
-e APP_KEY='' \
-e DD_AGENT_HOST='localhost' \
--name nest-test \
ethomatos/nest:v8

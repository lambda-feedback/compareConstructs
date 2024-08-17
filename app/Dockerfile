# Base image that bundles AWS Lambda Python 3.8 image with some middleware functions
# FROM base-eval-tmp
FROM rabidsheep55/python-base-eval-layer

WORKDIR /app

# Copy and install any packages/modules needed for your evaluation script.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY aifeedback.py ./app/
COPY compare.py ./app/
COPY evaluation.py ./app/
COPY evaluation_tests.py ./app/
COPY format.py ./app/
COPY general_check.py ./app/
COPY global_variable_check.py ./app/
COPY local_variable_check.py ./app/
COPY preview.py ./app/
COPY preview_tests.py ./app/
COPY param_generator.py ./app/
COPY structure_check.py ./app/
COPY same_variable_content_check.py ./app/

# Copy Documentation
COPY docs/dev.md ./app/docs/dev.md
COPY docs/user.md ./app/docs/user.md

# Set permissions so files and directories can be accessed on AWS
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)

# The entrypoint for AWS is to invoke the handler function within the app package
CMD [ "/app/app.handler" ]

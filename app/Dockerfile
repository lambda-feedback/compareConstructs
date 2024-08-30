# Base image that bundles AWS Lambda Python 3.8 image with some middleware functions
# FROM base-eval-tmp
FROM rabidsheep55/python-base-eval-layer

WORKDIR /app

# Copy and install any packages/modules needed for your evaluation script.
COPY requirements.txt .
RUN pip3 install -r requirements.txt



COPY utils/param_utils.py ./app/utils/

COPY format/variable_compare_format.py ./app/format/
COPY format/general_format.py ./app/format/
COPY format/output_traceback_format.py ./app/format/

COPY evaluation.py ./app/
COPY evaluation_tests.py ./app/

COPY checks/general_check.py ./app/checks/
COPY checks/global_variable_check.py ./app/checks/
COPY checks/local_variable_check.py ./app/checks/
COPY checks/structure_check.py ./app/checks/
COPY checks/same_variable_content_check.py ./app/checks/
COPY checks/ai_prompt_check.py ./app/checks/
COPY checks/check_result.py ./app/checks/
COPY checks/func_check.py ./app/checks/

COPY preview.py ./app/
COPY preview_tests.py ./app/



# Copy Documentation
COPY docs/dev.md ./app/docs/dev.md
COPY docs/user.md ./app/docs/user.md

# Set permissions so files and directories can be accessed on AWS
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)

# The entrypoint for AWS is to invoke the handler function within the app package
CMD [ "/app/app.handler" ]

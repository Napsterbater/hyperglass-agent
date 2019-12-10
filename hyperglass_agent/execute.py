# Standard Library Imports
import asyncio
import operator
from hyperglass_agent.exceptions import ExecutionError
from hyperglass_agent.nos_utils.bird import parse_bird_output
from hyperglass_agent.nos_utils.frr import parse_frr_output

# Third Party Imports
from logzero import logger as log

# Project Imports
from hyperglass_agent.config import commands
from hyperglass_agent.config import params


async def run_query(query):
    log.debug(f"Query: {query}")
    parser_map = {"bird": parse_bird_output, "frr": parse_frr_output}
    parser = parser_map[params.mode]

    command_raw = operator.attrgetter(
        ".".join([params.mode, query.afi, query.query_type])
    )(commands)

    log.debug(f"Raw Command: {command_raw}")

    command = command_raw.format(**query.dict())

    log.debug(f"Formatted Command: {command}")

    proc = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if stderr:
        raise ExecutionError(stderr.decode())

    if stdout:
        log.debug(f"Parser: {parser.__name__}")

        raw_output = stdout.decode()
        output = await parser(
            raw=raw_output, query_data=query, not_found=params.not_found_message
        )

    else:
        output = await parser(
            raw="", query_data=query, not_found=params.not_found_message
        )
    return output

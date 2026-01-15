Message(
  id='msg_01UaDWS6nSShhAoCMeEx58EY',
  content=[
    ThinkingBlock(
      signature='EpMECkYICxgCKkD7nmp7UA9HqBM9cnXQhjmem/PRkvyYtFBwNxGR3/IVCWGX3ponzfoviZdzovdovqX/DUfsBNjWSNHbVVI4q6iVEgwhWfGejBOZ2kLGWewaDPr1gqEb9CRm+ac5WSIwISC1APU74cKDLEXrrcm686VdSoHSwnFk/Px4uusg6umA6pcBRUca4FkDF48VsEWrKvoCLzVQ2vuc9OXbY0T0v8bvWb0JN2G4OUojQht5+jQhuvOht4HkHU8zWzDu5ZdsyxJzTo7jkYJCBN9skkOnJIVxUqya68iZ4D7BNmmlP2xbklM06UPQpPfm1k8gkGoYoaRFNX4Myzl4E8aOd3/wANSnh6HNVTmbxMJ2POKPDYzsu1XU9cWaqzo5FdWeLgnvZ+RMXKl3u/hllrEh0QAPtNV5k/oQSHev+sc+398HdpfTEm9KaYG+PK8t8+czCMFJsVPEo/JGULofP5PlrD+wHPuN3g4RnMpQrnFQjHn/iceaFK2+tfGN445L3rHDHN9JJuyTJFfRDRMUOaYz6WIlbgFAes/ZYrhF7kafdmuUpEY9XmT59bvE38DTJAdYb5lLOV6DnR2YkKNM5YzpJQRVpO7shhneYVxP2bhmF/bD+2epngC0BhaP3x1KPxK4E5d1GW+ftoVpVoZCg9i+qBYkmZ9t8nFy75IJfWVOwCILEdu1lB4BJw3Amhi/4+zNGAE=',
      thinking='The user is asking for a simple division calculation: 144 divided by 12. I have a calculate function available that can handle mathematical operations. I should use this tool to solve the problem.\n\nThe calculate function takes a "data" parameter which should be a string containing the mathematical expression. So I need to pass "144 / 12" as the data parameter.',
      type='thinking'
    ),
    TextBlock(
      citations=None,
      text="I'll calculate 144 divided by 12 for you using the calculation tool.",
      type='text'
    ),
    ToolUseBlock(
      id='toolu_01VwG3y7cxr8Qhb1MGorUZWk',
      input={'data': '144 / 12'},
      name='calculate',
      type='tool_use'
    )
  ],
  model='claude-sonnet-4-20250514',
  role='assistant',
  stop_reason='tool_use',
  stop_sequence=None,
  type='message',
  usage=Usage(
    cache_creation=CacheCreation(
      ephemeral_1h_input_tokens=0,
      ephemeral_5m_input_tokens=0
    ),
    cache_creation_input_tokens=0,
    cache_read_input_tokens=0,
    input_tokens=579,
    output_tokens=159,
    server_tool_use=None,
    service_tier='standard'
  )
)
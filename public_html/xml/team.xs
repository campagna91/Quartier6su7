<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
<xs:element name="team">
	<xs:complexType>
		<xs:sequence>
			<xs:element name="persona" maxOccurs="unbounded">
				<xs:complexType>
					<xs:sequence>
						<xs:element name="srcPath" type="xs:string"/>
						<xs:element name="nome" type="xs:string"/>
						<xs:element name="descr" type="xs:string"/>
						<xs:element name="presentazione" type="xs:string"/>
					</xs:sequence>
				</xs:complexType>
			</xs:element>
		</xs:sequence>
	</xs:complexType>
</xs:element>
</xs:schema>
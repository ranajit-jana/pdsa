import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Select, Table, Row, Col, message, Tag } from 'antd';
import { getRules, createRule, updateRule, getPIIEntities } from '../api'; // Import API methods
import './Page2.css';

const { Option } = Select;
const { TextArea } = Input;

const Page2 = () => {
  const [form] = Form.useForm();
  const [dataSource, setDataSource] = useState([]);
  const [entityOptions, setEntityOptions] = useState([]);
  const [selectedRecordKey, setSelectedRecordKey] = useState(null);
  const [entityMap, setEntityMap] = useState({}); // Create a state to hold the mapping of entity IDs to names

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [rulesData, entitiesData] = await Promise.all([getRules(), getPIIEntities()]);

      // Create a mapping of entity IDs to entity names
      const entityMap = {};
      entitiesData.forEach(entity => {
        entityMap[entity.entity_id] = entity.entity_name;
      });
      setEntityMap(entityMap);

      const processedData = rulesData.map((item) => {
        const combination = Array.isArray(item.entity_id)
          ? item.entity_id.map(id => entityMap[id]).join(', ')
          : '';

        return {
          key: item.rule_id,
          ruleName: item.rule_name,
          entities: item.entities, // Make sure entities are correctly populated here
          description: item.rule_description,
          score: item.score,
          rule_category: item.rule_category,
          entity_id: item.entity_id, // Store entity IDs for editing
        };
      });

      setDataSource(processedData);

      setEntityOptions(entitiesData.map(entity => ({
        value: entity.entity_id,
        label: entity.entity_name
      })));

    } catch (error) {
      message.error('Failed to fetch data');
      console.error('Fetch Error:', error);
    }
  };

  const handleFinish = async (values) => {
    try {
      // Map selected entity names from entityOptions to values.entity_names
      const selectedEntityNames = values.entity_names.map(name => {
        const option = entityOptions.find(option => option.label === name);
        return option ? option.label : null;
      }).filter(name => name !== null);
  
      // Create the payload object
      const payload = {
        rule_name: values.rule_name,
        entities: selectedEntityNames, // Use the selected entity names
        rule_description: values.rule_description,
        score: values.rule_score,
        rule_category: values.rule_category,
      };
  
      // Create new rule
      await createRule(payload);
  
      // Refetch rules data to get the latest data
      fetchData();
  
      message.success('Rule created successfully');
  
      // Reset form fields and selectedRecordKey
      form.resetFields();
      setSelectedRecordKey(null);
    } catch (error) {
      message.error('Failed to save rule');
      console.error('Save Error:', error);
    }
  };
  

  const handleCancel = () => {
    form.resetFields();
    setSelectedRecordKey(null);
  };

  const handleEdit = async (key) => {
    console.log(key);
    try {
      const record = dataSource.find((item) => item.key === key); // Assuming 'key' is the rule_id
      if (!record) {
        // If record is not found, display an error message
        message.error('Rule not found');
        return;
      }

      form.setFieldsValue({
        rule_name: record.ruleName,
        rule_description: record.description,
        rule_score: record.score,
        rule_category: record.rule_category,
        entity_names: record.entities, // Set entity names instead of entity IDs
      });
      setSelectedRecordKey(key);
    } catch (error) {
      message.error('Failed to fetch entity names');
      console.error('Fetch Error:', error);
    }
  };

  const columns = [
    {
      title: 'Rule name',
      dataIndex: 'ruleName',
      key: 'ruleName',
    },
    {
      title: 'Entities',
      dataIndex: 'entities',
      key: 'entities',
      render: entities => (
        <>
          {Array.isArray(entities) && entities.map(entity => (
            <Tag key={entity}>{entity}</Tag>
          ))}
        </>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Score',
      dataIndex: 'score',
      key: 'score',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button type="link" onClick={() => handleEdit(record.key)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <div>
      <h2>Rules</h2>
      <Form form={form} layout="vertical" onFinish={handleFinish}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Rule Name"
              name="rule_name"
              rules={[{ required: true, message: 'Please enter a rule name!' }]}
            >
              <Input placeholder="Enter rule name" disabled={selectedRecordKey !== null} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Rule Category"
              name="rule_category"
              rules={[{ required: true, message: 'Please select a rule category!' }]}
            >
              <Select placeholder="Select a rule category">
                <Option value="ID">Identity</Option>
                <Option value="FI">Financial</Option>
                <Option value="PR">Personal</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Rule Description"
              name="rule_description"
              rules={[{ required: true, message: 'Please enter a description!' }]}
            >
              <TextArea rows={2} placeholder="Enter description" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Rule Score"
              name="rule_score"
              rules={[{ required: true, message: 'Please select a score!' }]}
            >
              <Select placeholder="Select a score">
                {Array.from({ length: 10 }, (_, i) => (
                  <Option key={i + 1} value={i + 1}>{i + 1}</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={24}>
            <Form.Item
              label="Entities Names"
              name="entity_names"
              rules={[{ required: true, message: 'Please select entity names!' }]}
            >
              <Select mode="multiple" placeholder="Select entity names">
                {entityOptions.map(option => (
                  <Option key={option.label} value={option.label}>{option.label}</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save
          </Button>
          <Button style={{ marginLeft: '10px' }} onClick={handleCancel}>
            Cancel
          </Button>
        </Form.Item>
      </Form>
      <Table columns={columns} dataSource={dataSource} />
    </div>
  );
};

export default Page2;
